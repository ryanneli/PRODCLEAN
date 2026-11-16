using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class CertificadoRcpConfiguration : IEntityTypeConfiguration<CertificadoRcp>
{
    public void Configure(EntityTypeBuilder<CertificadoRcp> builder)
    {
        builder.ToTable("producao_certificadorcp");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Arquivo).IsRequired();
        builder.Property(x => x.NomeExibicao).HasMaxLength(255).IsRequired();
        builder.HasIndex(x => x.RcpId);
        builder.HasOne(x => x.Rcp).WithMany(x => x.Certificados).HasForeignKey(x => x.RcpId).OnDelete(DeleteBehavior.Cascade);
    }
}
