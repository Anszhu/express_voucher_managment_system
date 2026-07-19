import { Router } from 'express'; import { z } from 'zod'; import { asyncHandler, authenticate, validate } from '../middleware/core.js'; import * as auth from '../services/auth.service.js';
const router = Router(); const credentials = z.object({body:z.object({email:z.string().email(),password:z.string().min(8)}),query:z.any(),params:z.any()});
router.post('/login', validate(credentials), asyncHandler(async(req,res)=>res.json(await auth.login(req.body.email,req.body.password))));
router.post('/refresh', validate(z.object({body:z.object({refreshToken:z.string().min(1)}),query:z.any(),params:z.any()})), asyncHandler(async(req,res)=>res.json(await auth.refresh(req.body.refreshToken))));
router.post('/logout', authenticate, validate(z.object({body:z.object({refreshToken:z.string().min(1)}),query:z.any(),params:z.any()})), asyncHandler(async(req,res)=>{await auth.revoke(req.body.refreshToken);res.status(204).send();}));
router.get('/me', authenticate, asyncHandler(async (req,res) => res.json({ user: await auth.currentUser(req.auth!.id) })));
export default router;
