namespace ApiClean.Dominio.Entities;

public class Usuario
{
    public int Id { get; set; }
    public string NomeUsuario { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string SenhaHash { get; set; } = string.Empty;
    public bool Ativo { get; set; } = true;
    public DateTime CriadoEm { get; set; }
    public ICollection<UsuarioGrupo> Grupos { get; set; } = new List<UsuarioGrupo>();
}
