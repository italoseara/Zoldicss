import { BaseEntity, Column, CreateDateColumn, Entity, PrimaryColumn } from "typeorm";

@Entity("player")
class Player extends BaseEntity {
  @PrimaryColumn({ generated: "increment" })
  id: number;

  @Column({ unique: true, length: 18 })
  discordId: string;

  @Column({ default: 100 })
  health: number;

  @Column({ default: 100 })
  hunger: number;

  @Column({ default: 0 })
  experience: number;

  @Column({ default: 0, type: "bigint" })
  coins: bigint;

  @CreateDateColumn()
  createdAt: Date;
}

export default Player;
