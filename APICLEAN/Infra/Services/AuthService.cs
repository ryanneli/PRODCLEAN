using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using ApiClean.Application.DTO;
using ApiClean.Application.Interfaces;
using ApiClean.Dominio.Entities;
using ApiClean.Infra.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;

namespace ApiClean.Infra.Services;

public sealed class AuthService(
    AppDbContext context,
    IRcpPermissaoService rcpPermissaoService,
    IConfiguration configuration) : IAuthService
{
    private readonly PasswordHasher<Usuario> passwordHasher = new();

    public async Task<AuthResponseDto> RegistrarAsync(RegisterDto dto, CancellationToken cancellationToken = default)
    {
        var nomeUsuario = dto.NomeUsuario.Trim();
        var email = dto.Email.Trim();
        var grupoNome = dto.Grupo.Trim();

        if (string.IsNullOrWhiteSpace(nomeUsuario) ||
            string.IsNullOrWhiteSpace(email) ||
            string.IsNullOrWhiteSpace(dto.Senha))
        {
            throw new ArgumentException("Nome de usuário, e-mail e senha são obrigatórios.");
        }

        if (!rcpPermissaoService.GrupoValido(grupoNome))
        {
            throw new ArgumentException("Grupo inválido. Use Comercial, Qualidade ou Producao.");
        }

        if (await context.Usuarios.AnyAsync(x => x.NomeUsuario == nomeUsuario, cancellationToken))
        {
            throw new InvalidOperationException("Nome de usuário já cadastrado.");
        }

        if (await context.Usuarios.AnyAsync(x => x.Email == email, cancellationToken))
        {
            throw new InvalidOperationException("E-mail já cadastrado.");
        }

        var grupo = await context.GruposUsuarios
            .SingleOrDefaultAsync(
                x => x.Nome.ToLower() == grupoNome.ToLower(),
                cancellationToken);
        if (grupo is null)
        {
            throw new InvalidOperationException("O grupo informado não foi inicializado no banco de dados.");
        }
        var usuario = new Usuario
        {
            NomeUsuario = nomeUsuario,
            Email = email,
            CriadoEm = DateTime.UtcNow
        };
        usuario.SenhaHash = passwordHasher.HashPassword(usuario, dto.Senha);
        usuario.Grupos.Add(new UsuarioGrupo { Usuario = usuario, Grupo = grupo });

        await context.Usuarios.AddAsync(usuario, cancellationToken);
        await context.SaveChangesAsync(cancellationToken);

        return CriarResposta(usuario, grupo.Nome);
    }

    public async Task<AuthResponseDto?> LoginAsync(LoginDto dto, CancellationToken cancellationToken = default)
    {
        var usuario = await context.Usuarios
            .Include(x => x.Grupos)
                .ThenInclude(x => x.Grupo)
            .SingleOrDefaultAsync(x => x.NomeUsuario == dto.NomeUsuario, cancellationToken);

        if (usuario is null || !usuario.Ativo || usuario.Grupos.Count == 0)
        {
            return null;
        }

        var resultado = passwordHasher.VerifyHashedPassword(usuario, usuario.SenhaHash, dto.Senha);
        if (resultado == PasswordVerificationResult.Failed)
        {
            return null;
        }

        return CriarResposta(usuario, usuario.Grupos.First().Grupo.Nome);
    }

    private AuthResponseDto CriarResposta(Usuario usuario, string grupo)
    {
        var (token, expiraEm) = CriarToken(usuario, grupo);
        return new AuthResponseDto(
            token,
            expiraEm,
            usuario.NomeUsuario,
            grupo,
            rcpPermissaoService.ObterCamposVisiveis(),
            rcpPermissaoService.ObterCamposEditaveis(grupo));
    }

    private (string Token, DateTime ExpiraEm) CriarToken(Usuario usuario, string grupo)
    {
        var key = configuration["Jwt:Key"]
            ?? throw new InvalidOperationException("A configuração Jwt:Key deve ser definida.");
        var issuer = configuration["Jwt:Issuer"]
            ?? throw new InvalidOperationException("A configuração Jwt:Issuer deve ser definida.");
        var audience = configuration["Jwt:Audience"]
            ?? throw new InvalidOperationException("A configuração Jwt:Audience deve ser definida.");
        var minutos = configuration.GetValue("Jwt:ExpirationMinutes", 60);
        var expiraEm = DateTime.UtcNow.AddMinutes(minutos);
        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, usuario.Id.ToString()),
            new Claim(ClaimTypes.Name, usuario.NomeUsuario),
            new Claim(ClaimTypes.Role, grupo),
            new Claim("grupo", grupo)
        };
        var credentials = new SigningCredentials(
            new SymmetricSecurityKey(Encoding.UTF8.GetBytes(key)),
            SecurityAlgorithms.HmacSha256);
        var token = new JwtSecurityToken(
            issuer,
            audience,
            claims,
            expires: expiraEm,
            signingCredentials: credentials);

        return (new JwtSecurityTokenHandler().WriteToken(token), expiraEm);
    }
}
