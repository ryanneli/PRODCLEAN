namespace ApiClean.Dominio.Entities;

public class NotificacaoSetor
{
    public int Id { get; set; }
    public string SetorDestino { get; set; } = string.Empty;
    public string Mensagem { get; set; } = string.Empty;
    public DateTime DataCriacao { get; set; }
    public string RcpNumero { get; set; } = string.Empty;
    public ICollection<NotificacaoSetorUsuario> UsuariosQueLeram { get; set; } = new List<NotificacaoSetorUsuario>();
}
