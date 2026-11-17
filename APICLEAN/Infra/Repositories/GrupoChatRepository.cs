using ApiClean.Application.Interfaces;
using ApiClean.Dominio.Entities;
using ApiClean.Infra.Data;
using Microsoft.EntityFrameworkCore;

namespace ApiClean.Infra.Repositories;

public class GrupoChatRepository(AppDbContext context) : IGrupoChatRepository
{
    public Task<GrupoChat?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default) =>
        context.GruposChat.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public Task<GrupoChat?> ObterComRelacionamentosAsync(int id, CancellationToken cancellationToken = default) =>
        context.GruposChat.AsNoTracking().AsSplitQuery()
            .Include(x => x.Membros)
            .Include(x => x.Mensagens)
            .FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task<IReadOnlyList<GrupoChat>> ListarTodosAsync(CancellationToken cancellationToken = default) =>
        await context.GruposChat.AsNoTracking().OrderByDescending(x => x.CriadoEm).ToListAsync(cancellationToken);

    public async Task<IReadOnlyList<GrupoChat>> ListarPorUsuarioAsync(int usuarioId, CancellationToken cancellationToken = default) =>
        await context.GruposChat.AsNoTracking().Where(x => x.Membros.Any(m => m.UsuarioId == usuarioId))
            .OrderByDescending(x => x.CriadoEm).ToListAsync(cancellationToken);

    public Task<GrupoChat?> ObterChatPrivadoAsync(int usuario1Id, int usuario2Id, CancellationToken cancellationToken = default) =>
        context.GruposChat.AsNoTracking().AsSplitQuery()
            .Include(x => x.Membros)
            .Where(x => !x.EGrupo
                && x.Membros.Any(m => m.UsuarioId == usuario1Id)
                && x.Membros.Any(m => m.UsuarioId == usuario2Id)
                && x.Membros.Count == 2)
            .FirstOrDefaultAsync(cancellationToken);

    public async Task AdicionarAsync(GrupoChat entidade, CancellationToken cancellationToken = default) =>
        await context.GruposChat.AddAsync(entidade, cancellationToken);

    public void Atualizar(GrupoChat entidade) => context.GruposChat.Update(entidade);

    public void Remover(GrupoChat entidade) => context.GruposChat.Remove(entidade);

    public Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default) =>
        context.SaveChangesAsync(cancellationToken);
}
