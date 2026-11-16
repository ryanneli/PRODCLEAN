namespace ApiClean.Dominio.Entities;

public class GrupoChat
{
    public int Id { get; set; }
    public string? Nome { get; set; }
    public DateTime CriadoEm { get; set; }
    public bool EGrupo { get; set; }
    public ICollection<GrupoChatUsuario> Membros { get; set; } = new List<GrupoChatUsuario>();
    public ICollection<Mensagem> Mensagens { get; set; } = new List<Mensagem>();
}
