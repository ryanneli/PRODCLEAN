using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class QuadroObrasConfiguration : IEntityTypeConfiguration<QuadroObras>
{
    public void Configure(EntityTypeBuilder<QuadroObras> builder)
    {
        builder.ToTable("producao_quadroobras");
        builder.HasKey(x => x.OsObra);
        builder.Property(x => x.Cliente).HasMaxLength(100).IsRequired();
        builder.HasIndex(x => x.Cliente);
    }
}
