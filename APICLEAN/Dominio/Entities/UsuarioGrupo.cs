namespace ApiClean.Dominio.Entities;

public class UsuarioGrupo
{
    public int UsuarioId { get; set; }
    public int GrupoUsuarioId { get; set; }
    public Usuario Usuario { get; set; } = null!;
    public GrupoUsuario Grupo { get; set; } = null!;
}
