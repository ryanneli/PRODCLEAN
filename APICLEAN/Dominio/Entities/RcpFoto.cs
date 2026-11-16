namespace ApiClean.Dominio.Entities;

public class RcpFoto
{
    public int Id { get; set; }
    public int RcpId { get; set; }
    public string Imagem { get; set; } = string.Empty;
    public DateTime DataUpload { get; set; }
    public string Tipo { get; set; } = "antes";
    public OrdemServico Rcp { get; set; } = null!;
}
