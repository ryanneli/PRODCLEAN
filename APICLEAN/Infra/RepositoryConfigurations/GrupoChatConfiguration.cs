using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class GrupoChatConfiguration : IEntityTypeConfiguration<GrupoChat>
{
    public void Configure(EntityTypeBuilder<GrupoChat> builder)
    {
        builder.ToTable("producao_grupochat");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Nome).HasMaxLength(150);
        builder.HasIndex(x => x.EGrupo);
    }
}
