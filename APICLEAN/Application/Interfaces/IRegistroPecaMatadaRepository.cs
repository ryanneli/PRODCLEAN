using ApiClean.Dominio.Entities;

namespace ApiClean.Application.Interfaces;

public interface IRegistroPecaMatadaRepository
{
    Task<RegistroPecaMatada?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default);
    Task<RegistroPecaMatada?> ObterComRelacionamentosAsync(int id, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<RegistroPecaMatada>> ListarTodosAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<RegistroPecaMatada>> ListarPorFuncionarioAsync(int funcionarioId, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<RegistroPecaMatada>> ListarPorOrdemServicoAsync(int rcp, CancellationToken cancellationToken = default);
    Task AdicionarAsync(RegistroPecaMatada entidade, CancellationToken cancellationToken = default);
    void Atualizar(RegistroPecaMatada entidade);
    void Remover(RegistroPecaMatada entidade);
    Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default);
}
