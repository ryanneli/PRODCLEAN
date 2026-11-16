namespace ApiClean.Dominio.Entities;

public class Mensagem
{
    public int Id { get; set; }
    public int GrupoId { get; set; }
    public int AutorId { get; set; }
    public string Texto { get; set; } = string.Empty;
    public DateTime DataEnvio { get; set; }
    public bool Editada { get; set; }
    public DateTime? DataEdicao { get; set; }
    public bool Lida { get; set; }
    public GrupoChat Grupo { get; set; } = null!;
    public ICollection<LogEdicaoMensagem> HistoricoEdicoes { get; set; } = new List<LogEdicaoMensagem>();
}
