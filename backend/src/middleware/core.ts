import type { NextFunction, Request, Response } from 'express';
import jwt from 'jsonwebtoken';
import { ZodError, type ZodType } from 'zod';
import { config } from '../lib/config.js';
import { AppError } from '../lib/errors.js';
import { Role } from '@prisma/client';
export const asyncHandler = (fn: (req: Request, res: Response, next: NextFunction) => Promise<unknown>) => (req: Request, res: Response, next: NextFunction) => Promise.resolve(fn(req,res,next)).catch(next);
export const validate = (schema: ZodType) => (req: Request, _res: Response, next: NextFunction) => { try { schema.parse({ body: req.body, query: req.query, params: req.params }); next(); } catch (error) { next(error); } };
export const authenticate = (req: Request, _res: Response, next: NextFunction) => { try { const token = req.headers.authorization?.replace(/^Bearer\s+/i, ''); if (!token) throw new AppError(401, 'Authentication required'); const payload = jwt.verify(token, config.accessSecret) as Request['auth']; req.auth = payload; next(); } catch { next(new AppError(401, 'Invalid or expired access token')); } };
export const authorize = (...roles: Role[]) => (req: Request, _res: Response, next: NextFunction) => !req.auth ? next(new AppError(401, 'Authentication required')) : roles.includes(req.auth.role) ? next() : next(new AppError(403, 'Insufficient permission'));
export const notFound = (_req: Request, _res: Response, next: NextFunction) => next(new AppError(404, 'Route not found'));
export const errorHandler = (error: unknown, req: Request, res: Response, _next: NextFunction) => {
  const timestamp = new Date().toISOString();
  if (error instanceof ZodError) return res.status(422).json({ success: false, message: 'Validation failed', errorCode: 'VALIDATION_ERROR', errors: error.flatten(), timestamp, requestId: req.id });
  const known = error instanceof AppError ? error : new AppError(500, 'Internal server error');
  if (known.status >= 500) req.log.error({ err: error, requestId: req.id }, 'Unhandled request error');
  return res.status(known.status).json({ success: false, message: known.message, errorCode: known.status === 401 ? 'UNAUTHENTICATED' : known.status === 403 ? 'FORBIDDEN' : known.status === 404 ? 'NOT_FOUND' : 'REQUEST_ERROR', timestamp, requestId: req.id });
};
