using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class MensagemConfiguration : IEntityTypeConfiguration<Mensagem>
{
    public void Configure(EntityTypeBuilder<Mensagem> builder)
    {
        builder.ToTable("producao_mensagem");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Texto).IsRequired();
        builder.HasIndex(x => x.GrupoId);
        builder.HasIndex(x => x.AutorId);
        builder.HasOne(x => x.Grupo).WithMany(x => x.Mensagens).HasForeignKey(x => x.GrupoId).OnDelete(DeleteBehavior.Cascade);
    }
}
