namespace ApiClean.Dominio.Entities;

public class GrupoChatUsuario
{
    public int GrupoChatId { get; set; }
    public int UsuarioId { get; set; }
    public GrupoChat GrupoChat { get; set; } = null!;
}
