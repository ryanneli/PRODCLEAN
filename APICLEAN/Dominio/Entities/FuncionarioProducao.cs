namespace ApiClean.Dominio.Entities;

public class FuncionarioProducao
{
    public int Id { get; set; }
    public string Nome { get; set; } = string.Empty;
    public bool Ativo { get; set; } = true;
    public DateTime CriadoEm { get; set; }
    public ICollection<RegistroPecaMatada> Perdas { get; set; } = new List<RegistroPecaMatada>();
}
