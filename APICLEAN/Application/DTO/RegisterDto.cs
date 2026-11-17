namespace ApiClean.Application.DTO;

public sealed record RegisterDto(
    string NomeUsuario,
    string Email,
    string Senha,
    string Grupo);
