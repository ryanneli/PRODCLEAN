namespace ApiClean.Application.DTO;

public sealed record LoginDto(
    string NomeUsuario,
    string Senha);
