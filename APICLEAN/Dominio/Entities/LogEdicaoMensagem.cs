namespace ApiClean.Dominio.Entities;

public class LogEdicaoMensagem
{
    public int Id { get; set; }
    public int MensagemId { get; set; }
    public string TextoAntigo { get; set; } = string.Empty;
    public DateTime DataAlteracao { get; set; }
    public Mensagem Mensagem { get; set; } = null!;
}
