using ApiClean.Application.Interfaces;
using ApiClean.Dominio.Entities;
using ApiClean.Infra.Data;
using Microsoft.EntityFrameworkCore;

namespace ApiClean.Infra.Repositories;

public class OrdemServicoRepository(AppDbContext context) : IOrdemServicoRepository
{
    public Task<OrdemServico?> ObterPorIdAsync(int rcp, CancellationToken cancellationToken = default) =>
        context.OrdensServico.AsNoTracking().FirstOrDefaultAsync(x => x.Rcp == rcp, cancellationToken);

    public Task<OrdemServico?> ObterPorOsAsync(string os, CancellationToken cancellationToken = default) =>
        context.OrdensServico.AsNoTracking().FirstOrDefaultAsync(x => x.Os == os, cancellationToken);

    public Task<OrdemServico?> ObterComRelacionamentosAsync(int rcp, CancellationToken cancellationToken = default) =>
        context.OrdensServico.AsNoTracking().AsSplitQuery()
            .Include(x => x.Certificados)
            .Include(x => x.Fotos)
            .Include(x => x.PerdasPecas)
                .ThenInclude(x => x.Funcionario)
            .FirstOrDefaultAsync(x => x.Rcp == rcp, cancellationToken);

    public async Task<IReadOnlyList<OrdemServico>> ListarTodosAsync(CancellationToken cancellationToken = default) =>
        await context.OrdensServico.AsNoTracking().OrderBy(x => x.Rcp).ToListAsync(cancellationToken);

    public async Task AdicionarAsync(OrdemServico entidade, CancellationToken cancellationToken = default) =>
        await context.OrdensServico.AddAsync(entidade, cancellationToken);

    public void Atualizar(OrdemServico entidade) => context.OrdensServico.Update(entidade);

    public void Remover(OrdemServico entidade) => context.OrdensServico.Remove(entidade);

    public Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default) =>
        context.SaveChangesAsync(cancellationToken);
}
