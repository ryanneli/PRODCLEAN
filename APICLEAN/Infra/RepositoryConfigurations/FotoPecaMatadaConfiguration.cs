using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class FotoPecaMatadaConfiguration : IEntityTypeConfiguration<FotoPecaMatada>
{
    public void Configure(EntityTypeBuilder<FotoPecaMatada> builder)
    {
        builder.ToTable("producao_fotopecamatada");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Tipo).HasMaxLength(50);
        builder.Property(x => x.Imagem).HasMaxLength(500).IsRequired();
        builder.HasIndex(x => x.RegistroId);
        builder.HasOne(x => x.Registro).WithMany(x => x.Fotos).HasForeignKey(x => x.RegistroId).OnDelete(DeleteBehavior.Cascade);
    }
}
