using ApiClean.Application.Interfaces;

namespace ApiClean.Infra.Services;

public sealed class RcpPermissaoService : IRcpPermissaoService
{
    private static readonly string[] Grupos = ["Comercial", "Qualidade", "Producao"];

    private static readonly string[] CamposVisiveis =
    [
        "rcp", "editando_por", "editando_desde", "version", "os", "cliente",
        "proposta", "nf_saida", "tipo_servico", "prioridade", "data_liberacao",
        "liberado_por", "observacao_comercial", "nf_cliente", "data_entrada_peca",
        "descricao_peca", "obs_qualidade", "previsao_entrega_qualidade",
        "data_inspecao_inicial", "nome_motorista", "placa_veiculo", "obs_expedicao",
        "data_expedicao", "expedido_por", "status", "inicio_producao", "operador",
        "previsao_conclusao_prod", "data_finaliza_producao", "obs_producao",
        "data_inspecao_final", "certificado_pdf"
    ];

    private static readonly IReadOnlyDictionary<string, string[]> CamposPorGrupo =
        new Dictionary<string, string[]>(StringComparer.OrdinalIgnoreCase)
        {
            ["Comercial"] =
            [
                "os", "proposta", "nf_saida", "tipo_servico", "prioridade",
                "data_liberacao", "observacao_comercial"
            ],
            ["Qualidade"] =
            [
                "rcp", "cliente", "nf_cliente", "data_entrada_peca",
                "descricao_peca", "obs_qualidade", "previsao_entrega_qualidade",
                "data_expedicao", "expedido_por", "data_inspecao_final",
                "data_inspecao_inicial", "nome_motorista", "placa_veiculo",
                "obs_expedicao"
            ],
            ["Producao"] =
            [
                "inicio_producao", "operador", "previsao_conclusao_prod",
                "data_finaliza_producao", "obs_producao"
            ]
        };

    public IReadOnlyList<string> ObterCamposVisiveis() => CamposVisiveis;

    public IReadOnlyList<string> ObterCamposEditaveis(string grupo, bool superusuario = false, bool novaRcp = false)
    {
        var campos = superusuario
            ? CamposVisiveis.ToList()
            : CamposPorGrupo.TryGetValue(grupo, out var permitidos)
                ? permitidos.ToList()
                : [];

        campos.Remove("liberado_por");
        campos.Remove("status");

        if (!novaRcp)
        {
            campos.Remove("rcp");
        }

        return campos;
    }

    public bool PodeEditarCampo(string grupo, string campo, bool superusuario = false, bool novaRcp = false) =>
        ObterCamposEditaveis(grupo, superusuario, novaRcp)
            .Contains(campo, StringComparer.OrdinalIgnoreCase);

    public bool GrupoValido(string grupo) =>
        Grupos.Contains(grupo, StringComparer.OrdinalIgnoreCase);
}
