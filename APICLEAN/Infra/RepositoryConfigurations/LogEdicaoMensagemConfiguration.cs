using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class LogEdicaoMensagemConfiguration : IEntityTypeConfiguration<LogEdicaoMensagem>
{
    public void Configure(EntityTypeBuilder<LogEdicaoMensagem> builder)
    {
        builder.ToTable("producao_logedicaomensagem");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.TextoAntigo).IsRequired();
        builder.HasIndex(x => x.MensagemId);
        builder.HasOne(x => x.Mensagem).WithMany(x => x.HistoricoEdicoes)
            .HasForeignKey(x => x.MensagemId).OnDelete(DeleteBehavior.Cascade);
    }
}
