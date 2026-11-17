using ApiClean.Dominio.Entities;

namespace ApiClean.Application.Interfaces;

public interface IFuncionarioProducaoRepository
{
    Task<FuncionarioProducao?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default);
    Task<FuncionarioProducao?> ObterPorNomeAsync(string nome, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<FuncionarioProducao>> ListarTodosAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<FuncionarioProducao>> ListarAtivosAsync(CancellationToken cancellationToken = default);
    Task AdicionarAsync(FuncionarioProducao entidade, CancellationToken cancellationToken = default);
    void Atualizar(FuncionarioProducao entidade);
    void Remover(FuncionarioProducao entidade);
    Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default);
}
