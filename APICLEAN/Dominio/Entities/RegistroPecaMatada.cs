namespace ApiClean.Dominio.Entities;

public class RegistroPecaMatada
{
    public int Id { get; set; }
    public int FuncionarioId { get; set; }
    public int Quantidade { get; set; }
    public DateTime DataOcorrencia { get; set; }
    public string? Motivo { get; set; }
    public string? Resolucao { get; set; }
    public int? OsRelacionadaId { get; set; }
    public FuncionarioProducao Funcionario { get; set; } = null!;
    public OrdemServico? OsRelacionada { get; set; }
    public ICollection<FotoPecaMatada> Fotos { get; set; } = new List<FotoPecaMatada>();
}
