using ApiClean.Application.Interfaces;
using ApiClean.Dominio.Entities;
using ApiClean.Infra.Data;
using Microsoft.EntityFrameworkCore;

namespace ApiClean.Infra.Repositories;

public class MensagemRepository(AppDbContext context) : IMensagemRepository
{
    public Task<Mensagem?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default) =>
        context.Mensagens.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public Task<Mensagem?> ObterComRelacionamentosAsync(int id, CancellationToken cancellationToken = default) =>
        context.Mensagens.AsNoTracking()
            .Include(x => x.Grupo)
            .Include(x => x.HistoricoEdicoes)
            .FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task<IReadOnlyList<Mensagem>> ListarTodosAsync(CancellationToken cancellationToken = default) =>
        await context.Mensagens.AsNoTracking().OrderByDescending(x => x.DataEnvio).ToListAsync(cancellationToken);

    public async Task<IReadOnlyList<Mensagem>> ListarPorGrupoAsync(int grupoId, CancellationToken cancellationToken = default) =>
        await context.Mensagens.AsNoTracking().Where(x => x.GrupoId == grupoId)
            .OrderBy(x => x.DataEnvio).ToListAsync(cancellationToken);

    public async Task<IReadOnlyList<LogEdicaoMensagem>> ListarHistoricoEdicoesAsync(int mensagemId, CancellationToken cancellationToken = default) =>
        await context.LogsEdicaoMensagem.AsNoTracking().Where(x => x.MensagemId == mensagemId)
            .OrderByDescending(x => x.DataAlteracao).ToListAsync(cancellationToken);

    public async Task AdicionarAsync(Mensagem entidade, CancellationToken cancellationToken = default) =>
        await context.Mensagens.AddAsync(entidade, cancellationToken);

    public void Atualizar(Mensagem entidade) => context.Mensagens.Update(entidade);

    public void Remover(Mensagem entidade) => context.Mensagens.Remove(entidade);

    public Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default) =>
        context.SaveChangesAsync(cancellationToken);
}
