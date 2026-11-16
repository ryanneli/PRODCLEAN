using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class FuncionarioProducaoConfiguration : IEntityTypeConfiguration<FuncionarioProducao>
{
    public void Configure(EntityTypeBuilder<FuncionarioProducao> builder)
    {
        builder.ToTable("producao_funcionarioproducao");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Nome).HasMaxLength(100).IsRequired();
        builder.HasIndex(x => x.Nome).IsUnique();
    }
}
