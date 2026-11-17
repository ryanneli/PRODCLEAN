using ApiClean.Dominio.Entities;

namespace ApiClean.Application.Interfaces;

public interface ICertificadoRcpRepository
{
    Task<CertificadoRcp?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<CertificadoRcp>> ListarTodosAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<CertificadoRcp>> ListarPorRcpAsync(int rcp, CancellationToken cancellationToken = default);
    Task AdicionarAsync(CertificadoRcp entidade, CancellationToken cancellationToken = default);
    void Atualizar(CertificadoRcp entidade);
    void Remover(CertificadoRcp entidade);
    Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default);
}
