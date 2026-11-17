using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;

namespace ApiClean.Infra.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<OrdemServico> OrdensServico => Set<OrdemServico>();
    public DbSet<CertificadoRcp> CertificadosRcp => Set<CertificadoRcp>();
    public DbSet<RcpFoto> RcpFotos => Set<RcpFoto>();
    public DbSet<NotificacaoSetor> NotificacoesSetor => Set<NotificacaoSetor>();
    public DbSet<NotificacaoSetorUsuario> NotificacoesSetorUsuarios => Set<NotificacaoSetorUsuario>();
    public DbSet<GrupoChat> GruposChat => Set<GrupoChat>();
    public DbSet<GrupoChatUsuario> GruposChatUsuarios => Set<GrupoChatUsuario>();
    public DbSet<Mensagem> Mensagens => Set<Mensagem>();
    public DbSet<LogEdicaoMensagem> LogsEdicaoMensagem => Set<LogEdicaoMensagem>();
    public DbSet<FuncionarioProducao> FuncionariosProducao => Set<FuncionarioProducao>();
    public DbSet<RegistroPecaMatada> RegistrosPecasMatadas => Set<RegistroPecaMatada>();
    public DbSet<FotoPecaMatada> FotosPecasMatadas => Set<FotoPecaMatada>();
    public DbSet<Usuario> Usuarios => Set<Usuario>();
    public DbSet<GrupoUsuario> GruposUsuarios => Set<GrupoUsuario>();
    public DbSet<UsuarioGrupo> UsuariosGrupos => Set<UsuarioGrupo>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
        base.OnModelCreating(modelBuilder);
    }
}
