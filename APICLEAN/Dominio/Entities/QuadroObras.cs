namespace ApiClean.Dominio.Entities;

public class QuadroObras
{
    public int OsObra { get; set; }
    public string Cliente { get; set; } = string.Empty;
    public string? DescricaoObra { get; set; }
    public DateTime? DataInicioObra { get; set; }
}
