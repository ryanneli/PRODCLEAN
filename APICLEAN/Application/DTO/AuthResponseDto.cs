namespace ApiClean.Application.DTO;

public sealed record AuthResponseDto(
    string Token,
    DateTime ExpiraEm,
    string NomeUsuario,
    string Grupo,
    IReadOnlyList<string> CamposVisiveisRcp,
    IReadOnlyList<string> CamposEditaveisRcp);
