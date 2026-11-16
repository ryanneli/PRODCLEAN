namespace ApiClean.Dominio.Entities;

public class CertificadoRcp
{
    public int Id { get; set; }
    public int RcpId { get; set; }
    public string Arquivo { get; set; } = string.Empty;
    public string NomeExibicao { get; set; } = string.Empty;
    public DateTime DataUpload { get; set; }
    public OrdemServico Rcp { get; set; } = null!;
}
