namespace ApiClean.Dominio.Entities;

public class OrdemServico
{
    public int Rcp { get; set; }
    public int? EditandoPorId { get; set; }
    public DateTime? EditandoDesde { get; set; }
    public int Version { get; set; }
    public string Os { get; set; } = "0000/26";
    public string Cliente { get; set; } = string.Empty;
    public string? Proposta { get; set; }
    public string? NfSaida { get; set; }
    public string? TipoServico { get; set; }
    public string Prioridade { get; set; } = "A SER DEFINIDO PELA COMERCIAL";
    public DateTime? DataLiberacao { get; set; }
    public string? LiberadoPor { get; set; }
    public string? ObservacaoComercial { get; set; }
    public string? NfCliente { get; set; }
    public DateTime? DataEntradaPeca { get; set; }
    public string? DescricaoPeca { get; set; }
    public string? ObsQualidade { get; set; }
    public DateTime? PrevisaoEntregaQualidade { get; set; }
    public DateTime? DataInspecaoInicial { get; set; }
    public string? NomeMotorista { get; set; }
    public string? PlacaVeiculo { get; set; }
    public string? ObsExpedicao { get; set; }
    public DateTime? DataExpedicao { get; set; }
    public string? ExpedidoPor { get; set; }
    public string Status { get; set; } = "AGUARDANDO LIBERAÇÃO";
    public DateTime? InicioProducao { get; set; }
    public string? Operador { get; set; }
    public DateTime? PrevisaoConclusaoProd { get; set; }
    public DateTime? DataFinalizaProducao { get; set; }
    public string? ObsProducao { get; set; }
    public DateTime? DataInspecaoFinal { get; set; }
    public string? CertificadoPdf { get; set; }

    public ICollection<CertificadoRcp> Certificados { get; set; } = new List<CertificadoRcp>();
    public ICollection<RcpFoto> Fotos { get; set; } = new List<RcpFoto>();
    public ICollection<RegistroPecaMatada> PerdasPecas { get; set; } = new List<RegistroPecaMatada>();
}
