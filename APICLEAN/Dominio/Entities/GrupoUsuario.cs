namespace ApiClean.Dominio.Entities;

public class GrupoUsuario
{
    public int Id { get; set; }
    public string Nome { get; set; } = string.Empty;
    public ICollection<UsuarioGrupo> Usuarios { get; set; } = new List<UsuarioGrupo>();
}
