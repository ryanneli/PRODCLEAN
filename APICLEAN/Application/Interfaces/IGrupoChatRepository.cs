using ApiClean.Dominio.Entities;

namespace ApiClean.Application.Interfaces;

public interface IGrupoChatRepository
{
    Task<GrupoChat?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default);
    Task<GrupoChat?> ObterComRelacionamentosAsync(int id, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<GrupoChat>> ListarTodosAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<GrupoChat>> ListarPorUsuarioAsync(int usuarioId, CancellationToken cancellationToken = default);
    Task<GrupoChat?> ObterChatPrivadoAsync(int usuario1Id, int usuario2Id, CancellationToken cancellationToken = default);
    Task AdicionarAsync(GrupoChat entidade, CancellationToken cancellationToken = default);
    void Atualizar(GrupoChat entidade);
    void Remover(GrupoChat entidade);
    Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default);
}
