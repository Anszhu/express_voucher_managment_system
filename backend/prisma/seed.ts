import { PrismaClient, Role } from '@prisma/client';
import bcrypt from 'bcryptjs';
const prisma = new PrismaClient();
const run = async () => {
  const passwordHash = await bcrypt.hash('ChangeMe123!', 12);
  for (const user of [
    ['employee@example.com', 'Demo Employee', Role.EMPLOYEE, 'Operations'],
    ['director@example.com', 'Demo Director', Role.DIRECTOR, 'Management'],
    ['accounts@example.com', 'Demo Accounts', Role.ACCOUNTS, 'Finance']
  ] as const) await prisma.user.upsert({ where: { email: user[0] }, update: {}, create: { email: user[0], name: user[1], role: user[2], department: user[3], passwordHash } });
};
run().then(() => prisma.$disconnect()).catch(async error => { console.error(error); await prisma.$disconnect(); process.exit(1); });
