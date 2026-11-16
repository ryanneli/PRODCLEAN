using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class GrupoChatUsuarioConfiguration : IEntityTypeConfiguration<GrupoChatUsuario>
{
    public void Configure(EntityTypeBuilder<GrupoChatUsuario> builder)
    {
        builder.ToTable("producao_grupochat_membros");
        builder.HasKey(x => new { x.GrupoChatId, x.UsuarioId });
        builder.HasIndex(x => x.UsuarioId);
        builder.HasOne(x => x.GrupoChat).WithMany(x => x.Membros)
            .HasForeignKey(x => x.GrupoChatId).OnDelete(DeleteBehavior.Cascade);
    }
}
