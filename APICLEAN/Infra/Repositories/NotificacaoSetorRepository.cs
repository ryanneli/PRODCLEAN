using ApiClean.Application.Interfaces;
using ApiClean.Dominio.Entities;
using ApiClean.Infra.Data;
using Microsoft.EntityFrameworkCore;

namespace ApiClean.Infra.Repositories;

public class NotificacaoSetorRepository(AppDbContext context) : INotificacaoSetorRepository
{
    public Task<NotificacaoSetor?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default) =>
        context.NotificacoesSetor.AsNoTracking().Include(x => x.UsuariosQueLeram)
            .FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task<IReadOnlyList<NotificacaoSetor>> ListarTodosAsync(CancellationToken cancellationToken = default) =>
        await context.NotificacoesSetor.AsNoTracking().OrderByDescending(x => x.DataCriacao).ToListAsync(cancellationToken);

    public async Task<IReadOnlyList<NotificacaoSetor>> ListarPorUsuarioAsync(int usuarioId, CancellationToken cancellationToken = default) =>
        await context.NotificacoesSetor.AsNoTracking().Where(x => x.UsuariosQueLeram.Any(u => u.UsuarioId == usuarioId))
            .OrderByDescending(x => x.DataCriacao).ToListAsync(cancellationToken);

    public async Task<IReadOnlyList<NotificacaoSetor>> ListarNaoLidasPorUsuarioAsync(int usuarioId, CancellationToken cancellationToken = default) =>
        await context.NotificacoesSetor.AsNoTracking().Where(x => !x.UsuariosQueLeram.Any(u => u.UsuarioId == usuarioId))
            .OrderByDescending(x => x.DataCriacao).ToListAsync(cancellationToken);

    public async Task AdicionarAsync(NotificacaoSetor entidade, CancellationToken cancellationToken = default) =>
        await context.NotificacoesSetor.AddAsync(entidade, cancellationToken);

    public void Atualizar(NotificacaoSetor entidade) => context.NotificacoesSetor.Update(entidade);

    public void Remover(NotificacaoSetor entidade) => context.NotificacoesSetor.Remove(entidade);

    public Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default) =>
        context.SaveChangesAsync(cancellationToken);
}
