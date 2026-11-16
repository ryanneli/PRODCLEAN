namespace ApiClean.Dominio.Entities;

public class NotificacaoSetorUsuario
{
    public int NotificacaoSetorId { get; set; }
    public int UsuarioId { get; set; }
    public NotificacaoSetor Notificacao { get; set; } = null!;
}
