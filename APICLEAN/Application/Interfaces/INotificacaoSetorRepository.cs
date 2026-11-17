using ApiClean.Dominio.Entities;

namespace ApiClean.Application.Interfaces;

public interface INotificacaoSetorRepository
{
    Task<NotificacaoSetor?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<NotificacaoSetor>> ListarTodosAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<NotificacaoSetor>> ListarPorUsuarioAsync(int usuarioId, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<NotificacaoSetor>> ListarNaoLidasPorUsuarioAsync(int usuarioId, CancellationToken cancellationToken = default);
    Task AdicionarAsync(NotificacaoSetor entidade, CancellationToken cancellationToken = default);
    void Atualizar(NotificacaoSetor entidade);
    void Remover(NotificacaoSetor entidade);
    Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default);
}
