using ApiClean.Dominio.Entities;

namespace ApiClean.Application.Interfaces;

public interface IOrdemServicoRepository
{
    Task<OrdemServico?> ObterPorIdAsync(int rcp, CancellationToken cancellationToken = default);
    Task<OrdemServico?> ObterPorOsAsync(string os, CancellationToken cancellationToken = default);
    Task<OrdemServico?> ObterComRelacionamentosAsync(int rcp, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<OrdemServico>> ListarTodosAsync(CancellationToken cancellationToken = default);
    Task AdicionarAsync(OrdemServico entidade, CancellationToken cancellationToken = default);
    void Atualizar(OrdemServico entidade);
    void Remover(OrdemServico entidade);
    Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default);
}
