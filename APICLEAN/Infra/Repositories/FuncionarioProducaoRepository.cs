using ApiClean.Application.Interfaces;
using ApiClean.Dominio.Entities;
using ApiClean.Infra.Data;
using Microsoft.EntityFrameworkCore;

namespace ApiClean.Infra.Repositories;

public class FuncionarioProducaoRepository(AppDbContext context) : IFuncionarioProducaoRepository
{
    public Task<FuncionarioProducao?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default) =>
        context.FuncionariosProducao.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public Task<FuncionarioProducao?> ObterPorNomeAsync(string nome, CancellationToken cancellationToken = default) =>
        context.FuncionariosProducao.AsNoTracking().FirstOrDefaultAsync(x => x.Nome == nome, cancellationToken);

    public async Task<IReadOnlyList<FuncionarioProducao>> ListarTodosAsync(CancellationToken cancellationToken = default) =>
        await context.FuncionariosProducao.AsNoTracking().OrderBy(x => x.Nome).ToListAsync(cancellationToken);

    public async Task<IReadOnlyList<FuncionarioProducao>> ListarAtivosAsync(CancellationToken cancellationToken = default) =>
        await context.FuncionariosProducao.AsNoTracking().Where(x => x.Ativo).OrderBy(x => x.Nome).ToListAsync(cancellationToken);

    public async Task AdicionarAsync(FuncionarioProducao entidade, CancellationToken cancellationToken = default) =>
        await context.FuncionariosProducao.AddAsync(entidade, cancellationToken);

    public void Atualizar(FuncionarioProducao entidade) => context.FuncionariosProducao.Update(entidade);

    public void Remover(FuncionarioProducao entidade) => context.FuncionariosProducao.Remove(entidade);

    public Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default) =>
        context.SaveChangesAsync(cancellationToken);
}
