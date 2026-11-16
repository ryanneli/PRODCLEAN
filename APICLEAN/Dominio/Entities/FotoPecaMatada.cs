namespace ApiClean.Dominio.Entities;

public class FotoPecaMatada
{
    public int Id { get; set; }
    public int RegistroId { get; set; }
    public string? Tipo { get; set; }
    public string Imagem { get; set; } = string.Empty;
    public DateTime DataUpload { get; set; }
    public RegistroPecaMatada Registro { get; set; } = null!;
}
