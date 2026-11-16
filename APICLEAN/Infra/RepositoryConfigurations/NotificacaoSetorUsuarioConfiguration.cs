using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class NotificacaoSetorUsuarioConfiguration : IEntityTypeConfiguration<NotificacaoSetorUsuario>
{
    public void Configure(EntityTypeBuilder<NotificacaoSetorUsuario> builder)
    {
        builder.ToTable("producao_notificacaosetor_usuarios_que_leram");
        builder.HasKey(x => new { x.NotificacaoSetorId, x.UsuarioId });
        builder.HasIndex(x => x.UsuarioId);
        builder.HasOne(x => x.Notificacao).WithMany(x => x.UsuariosQueLeram)
            .HasForeignKey(x => x.NotificacaoSetorId).OnDelete(DeleteBehavior.Cascade);
    }
}
