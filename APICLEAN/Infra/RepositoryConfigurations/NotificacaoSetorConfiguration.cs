using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class NotificacaoSetorConfiguration : IEntityTypeConfiguration<NotificacaoSetor>
{
    public void Configure(EntityTypeBuilder<NotificacaoSetor> builder)
    {
        builder.ToTable("producao_notificacaosetor");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.SetorDestino).HasMaxLength(20).IsRequired();
        builder.Property(x => x.RcpNumero).HasMaxLength(50).IsRequired();
        builder.HasIndex(x => x.DataCriacao);
        builder.HasIndex(x => x.RcpNumero);
    }
}
