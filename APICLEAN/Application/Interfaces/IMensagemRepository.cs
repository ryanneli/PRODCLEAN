using ApiClean.Dominio.Entities;

namespace ApiClean.Application.Interfaces;

public interface IMensagemRepository
{
    Task<Mensagem?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default);
    Task<Mensagem?> ObterComRelacionamentosAsync(int id, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<Mensagem>> ListarTodosAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<Mensagem>> ListarPorGrupoAsync(int grupoId, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<LogEdicaoMensagem>> ListarHistoricoEdicoesAsync(int mensagemId, CancellationToken cancellationToken = default);
    Task AdicionarAsync(Mensagem entidade, CancellationToken cancellationToken = default);
    void Atualizar(Mensagem entidade);
    void Remover(Mensagem entidade);
    Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default);
}
