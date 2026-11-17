using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class GrupoUsuarioConfiguration : IEntityTypeConfiguration<GrupoUsuario>
{
    public void Configure(EntityTypeBuilder<GrupoUsuario> builder)
    {
        builder.ToTable("GruposUsuarios");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Nome).HasMaxLength(50).IsRequired();
        builder.HasIndex(x => x.Nome).IsUnique();
    }
}
