import { Router } from 'express';
import { prisma } from '../lib/prisma.js';
import { asyncHandler, authenticate, authorize } from '../middleware/core.js';
import { Role } from '@prisma/client';

const router = Router();

router.use(authenticate);

// Only Directors and Accounts can list users
router.get('/', authorize(Role.DIRECTOR, Role.ACCOUNTS), asyncHandler(async (_req, res) => {
  const users = await prisma.user.findMany({
    where: { deletedAt: null, isActive: true },
    select: { id: true, email: true, name: true, role: true, department: true, isActive: true, createdAt: true },
    orderBy: { name: 'asc' },
  });
  res.json({ users });
}));

router.get('/:id', authorize(Role.DIRECTOR, Role.ACCOUNTS), asyncHandler(async (req, res) => {
  const user = await prisma.user.findFirst({
    where: { id: String(req.params.id), deletedAt: null, isActive: true },
    select: { id: true, email: true, name: true, role: true, department: true, isActive: true, createdAt: true, updatedAt: true },
  });
  if (!user) return res.status(404).json({ success: false, message: 'User not found' });
  res.json({ user });
}));

export default router;
