using ApiClean.Application.Interfaces;
using ApiClean.Dominio.Entities;
using ApiClean.Infra.Data;
using Microsoft.EntityFrameworkCore;

namespace ApiClean.Infra.Repositories;

public class CertificadoRcpRepository(AppDbContext context) : ICertificadoRcpRepository
{
    public Task<CertificadoRcp?> ObterPorIdAsync(int id, CancellationToken cancellationToken = default) =>
        context.CertificadosRcp.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task<IReadOnlyList<CertificadoRcp>> ListarTodosAsync(CancellationToken cancellationToken = default) =>
        await context.CertificadosRcp.AsNoTracking().OrderByDescending(x => x.DataUpload).ToListAsync(cancellationToken);

    public async Task<IReadOnlyList<CertificadoRcp>> ListarPorRcpAsync(int rcp, CancellationToken cancellationToken = default) =>
        await context.CertificadosRcp.AsNoTracking().Where(x => x.RcpId == rcp)
            .OrderByDescending(x => x.DataUpload).ToListAsync(cancellationToken);

    public async Task AdicionarAsync(CertificadoRcp entidade, CancellationToken cancellationToken = default) =>
        await context.CertificadosRcp.AddAsync(entidade, cancellationToken);

    public void Atualizar(CertificadoRcp entidade) => context.CertificadosRcp.Update(entidade);

    public void Remover(CertificadoRcp entidade) => context.CertificadosRcp.Remove(entidade);

    public Task<int> SalvarAlteracoesAsync(CancellationToken cancellationToken = default) =>
        context.SaveChangesAsync(cancellationToken);
}
