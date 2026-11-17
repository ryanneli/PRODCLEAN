namespace ApiClean.Application.Interfaces;

public interface IRcpPermissaoService
{
    IReadOnlyList<string> ObterCamposVisiveis();
    IReadOnlyList<string> ObterCamposEditaveis(string grupo, bool superusuario = false, bool novaRcp = false);
    bool PodeEditarCampo(string grupo, string campo, bool superusuario = false, bool novaRcp = false);
    bool GrupoValido(string grupo);
}
