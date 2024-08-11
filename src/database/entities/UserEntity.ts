import { BaseEntity, Column, Entity, PrimaryColumn } from "typeorm";

@Entity("user")
class UserEntity extends BaseEntity {
  @PrimaryColumn()
  id: number;

  @Column({ unique: true, length: 18 })
  discordId: string;
}

export default UserEntity;
