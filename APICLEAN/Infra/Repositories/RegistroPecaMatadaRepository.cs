using ApiClean.Application.Interfaces;
using ApiClean.Dominio.Entities;
using ApiClean.Infra.Data;
using Microsoft.EntityFrameworkCore;

namespace ApiClean.Infra.Repositories;

public class RegistroPecaMatadaRepository(AppDbContext context) : IRegistroPecaMatadaRepository
{
    public Task<RegistroPecaMatada?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default) =>
        context.RegistrosPecasMatadas.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public Task<RegistroPecaMatada?> ObterComRelacionamentosAsync(int id, CancellationToken cancellationToken = default) =>
        context.RegistrosPecasMatadas.AsNoTracking()
            .Include(x => x.Funcionario)
            .Include(x => x.OsRelacionada)
            .Include(x => x.Fotos)
            .FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task<IReadOnlyList<RegistroPecaMatada>> ListarTodosAsync(CancellationToken cancellationToken = default) =>
        await context.RegistrosPecasMatadas.AsNoTracking().AsSplitQuery()
            .Include(x => x.Funcionario).Include(x => x.Fotos)
            .OrderByDescending(x => x.DataOcorrencia).ToListAsync(cancellationToken);

    public async Task<IReadOnlyList<RegistroPecaMatada>> ListarPorFuncionarioAsync(int funcionarioId, CancellationToken cancellationToken = default) =>
        await context.RegistrosPecasMatadas.AsNoTracking().Where(x => x.FuncionarioId == funcionarioId)
            .Include(x => x.Fotos).OrderByDescending(x => x.DataOcorrencia).ToListAsync(cancellationToken);

    public async Task<IReadOnlyList<RegistroPecaMatada>> ListarPorOrdemServicoAsync(int rcp, CancellationToken cancellationToken = default) =>
        await context.RegistrosPecasMatadas.AsNoTracking().Where(x => x.OsRelacionadaId == rcp)
            .Include(x => x.Funcionario).Include(x => x.Fotos)
            .OrderByDescending(x => x.DataOcorrencia).ToListAsync(cancellationToken);

    public async Task AdicionarAsync(RegistroPecaMatada entidade, CancellationToken cancellationToken = default) =>
        await context.RegistrosPecasMatadas.AddAsync(entidade, cancellationToken);

    public void Atualizar(RegistroPecaMatada entidade) => context.RegistrosPecasMatadas.Update(entidade);

    public void Remover(RegistroPecaMatada entidade) => context.RegistrosPecasMatadas.Remove(entidade);

    public Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default) =>
        context.SaveChangesAsync(cancellationToken);
}
