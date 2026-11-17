
using ApiClean.Dominio.Entities;
using ApiClean.Infra.Data;
using Microsoft.EntityFrameworkCore;

namespace ApiClean.Infra.Services;

public sealed class DatabaseSeeder(AppDbContext context)
{
    private static readonly string[] GruposLegado = ["Comercial", "Qualidade", "Producao"];

    public async Task SeedAsync(CancellationToken cancellationToken = default)
    {
        await context.Database.EnsureCreatedAsync(cancellationToken);

        foreach (var nome in GruposLegado)
        {
            if (!await context.GruposUsuarios.AnyAsync(x => x.Nome == nome, cancellationToken))
            {
                await context.GruposUsuarios.AddAsync(
                    new GrupoUsuario { Nome = nome },
                    cancellationToken);
            }
        }

        await context.SaveChangesAsync(cancellationToken);
    }
}
