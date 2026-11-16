using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class RcpFotoConfiguration : IEntityTypeConfiguration<RcpFoto>
{
    public void Configure(EntityTypeBuilder<RcpFoto> builder)
    {
        builder.ToTable("producao_rcpfoto");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Imagem).HasMaxLength(500).IsRequired();
        builder.Property(x => x.Tipo).HasMaxLength(10).IsRequired();
        builder.HasIndex(x => x.RcpId);
        builder.HasOne(x => x.Rcp).WithMany(x => x.Fotos).HasForeignKey(x => x.RcpId).OnDelete(DeleteBehavior.Cascade);
    }
}
